FROM archlinux:latest
RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm --needed figlet banner cowsay openssh sudo which
WORKDIR /stuff
COPY . .
RUN chmod +x ./do.sh
CMD ["./do.sh"]
