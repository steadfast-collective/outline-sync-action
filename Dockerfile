FROM python:3.8

# ---
# Project specific
# ---
WORKDIR /gfmd
COPY . .

RUN python3.8 -m pip install .

# ---
# Entry point stuff
# ---
ENV ENTRYPOINT_PATH /gfmd
ENTRYPOINT ["gfmd"]
CMD [ "--help" ]
