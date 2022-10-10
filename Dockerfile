FROM python:3.6-slim

WORKDIR /root/Repos/dotfiles
COPY . ./

RUN ["python", ".sym_links.py", "debug"]
