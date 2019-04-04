import os
import jinja2
import tempfile
from repo2docker.buildpacks.docker import DockerBuildPack


class PangeoStackBuildPack(DockerBuildPack):
    DOCKERFILE_TEMPLATE = r"""
    FROM {{ image_spec }}

    COPY --chown=1000:1000 . ${REPO_DIR}

    {% if files["environment.yml"] %}
    RUN conda env update -n root -f {{ files["environment.yml"] }} && \
        conda clean -tipsy && \
        conda list -n root
    {% endif %}

    {% if files["postBuild"] %}
    RUN chmod +x {{ files["postBuild"] }}
    RUN ./{{ files["postBuild"] }}
    {% endif %}

    {% if files["start"] %}
    RUN chmod +x {{ files["start"] }}
    ENTRYPOINT [ "{{ files["start"] }}" ]
    {% endif %}
    """
    def detect(self):
        stack_path = self.binder_path('pangeo-stack')
        if os.path.exists(stack_path):
            with open(stack_path) as f:
                stack = f.read().strip()

            if not stack.startswith('pangeo/'):
                return False

            if not ':' in stack:
                return False

            if ':latest' in stack:
                return False

            return True

    def render(self):
        with open(self.binder_path('pangeo-stack')) as f:
            pangeo_stack = f.read().strip()


        environment_file = postbuild_file = requirements_file = start_file = None

        files = {
            'environment.yml': None,
            'postBuild': None,
            'start': None
        }

        for filename in files:
            if os.path.exists(self.binder_path(filename)):
                files[filename] = self.binder_path(filename)

        t = jinja2.Template(PangeoStackBuildPack.DOCKERFILE_TEMPLATE)

        return t.render(
            image_spec=pangeo_stack,
            files=files
        )

    def build(self, *args, **kwargs):
        with tempfile.NamedTemporaryFile() as f:
            f.write(self.render().encode('utf-8'))
            f.flush()

            self.dockerfile = f.name

            yield from super().build(*args, **kwargs)