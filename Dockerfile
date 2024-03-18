FROM python:3.10-slim

WORKDIR /root/Repos/dotfiles
COPY . ./

RUN ["python", "dotfiles.py", "-dsm", "."]
