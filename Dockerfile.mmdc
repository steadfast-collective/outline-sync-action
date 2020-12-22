FROM minlag/mermaid-cli:8.8.4

# ---
# Setup python for glue code
# ---
RUN apt-get update && \
apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev \
    && curl -O https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tar.xz \
    && tar -xf Python-3.8.2.tar.xz \
    && cd Python-3.8.2 \
    && ./configure --enable-optimizations \
    && make -j 4 \
    && make altinstall \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge --auto-remove -y curl \
    && rm -rf /src/*.deb

RUN python3.8 -m pip install pip --upgrade && python3.8 -m pip install pipenv

# ---
# Project specific
# ---
WORKDIR /gfmd

COPY Pipfile* ./
RUN pipenv install --system --deploy

COPY . .

# ---
# Entry point stuff
# ---
ENV ENTRYPOINT_PATH /gfmd
ENTRYPOINT ["/gfmd/src/markdown_process" ]
CMD [ "--help" ]
