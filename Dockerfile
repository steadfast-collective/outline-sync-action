FROM python:3.8

# ---
# Project specific
# ---
WORKDIR /gfmd
COPY . .

# ---
# Entry point stuff
# ---
ENV ENTRYPOINT_PATH /gfmd
ENTRYPOINT ["/gfmd/src/markdown_process" ]
CMD [ "--help" ]
