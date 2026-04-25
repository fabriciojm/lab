# Create user in Linux (inside Alpine container)

I'm writing in my blog that the ultimate Linux beginner task for me was creating a Linux user by hand. I've done inside an Alpine container to refresh my memory.

```bash
docker run -it alpine
# Ideally one does this with VIm to learn editing
echo "fabricio:x:65533:65533:nobody:/home/fabricio:/bin/ash" >> /etc/passwd
echo "fabricio:*::0:::::" >> /etc/shadow
mkdir /home/fabricio
chown fabricio:nobody /home/fabricio
passwd fabricio
su - fabricio # should work
```
