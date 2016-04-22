FROM python:latest

MAINTAINER Caesar Kabalan <caesar.kabalan@gmail.com>

# Copy the code into the container
COPY . /losteyelid/checkexecutor/

# Upgrade pip
RUN pip install --upgrade pip

# Install prereqs with pip
RUN pip install -r /losteyelid/checkexecutor/requirements.txt

# Set the entrypoint to run the main method
CMD [ "python", "/losteyelid/checkexecutor/__main__.py" ]
