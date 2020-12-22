FROM python:3.8

RUN pip install --upgrade pip pipenv

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
