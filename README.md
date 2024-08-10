# ⚙️ SERVICE.BUTTON-HANDLER

![main_img](https://github.com/FUNCKA-TOASTER/service.button-handler/assets/76991612/40e1cb24-f2d0-4786-bf49-a8dabe0f35b2)

## 📄 Информация

**SERVICE.BUTTON-HANDLER** - сервис обработки событий, классифицированных как "button". Событие приходит от сервиса фетчинга через шину Redis, после чего обрабатывается, параллельно логируя свои дейстивия как внутри контейнера (внутренние логи), так и внутри лог-чатов (внешние логи).

### Входные данные

Пример обьекта события, которое приходит на service.button-handler:

```python
class Event:
    event_id: str
    event_type: str

    peer: Peer
    user: User
    button: Button
```

```python
class Button(NamedTuple):
    cmid: int
    beid: str
    payload: dict
```

```python
class Peer(NamedTuple):
    bpid: int
    cid: int
    name: str
```

```python
class User(NamedTuple):
    uuid: int
    name: str
    firstname: str
    lastname: str
    nick: str
```

Далее, сервис определяет имя вызвваемого действия внутри полезной нагрузки кнопки и исполняет его, имспользуя атрибуты, которые также были заложены внутри полезной нагрузки.

### Дополнительно

Docker setup:

```shell
    docker network
        name: TOASTER
        ip_gateway: 172.18.0.1
        subnet: 172.18.0.0/16
        driver: bridge
    

    docker image
        name: service.button-handler
        args:
            TOKEN: "..."
            GROUPID: "..."
            SQL_HOST: "..."
            SQL_PORT: "..."
            SQL_USER: "..."
            SQL_PSWD: "..."
    

    docker container
        name: service.button-handler
        network_ip: 172.1.08.7
```

Jenkisn shell command:

```shell
imageName="service.button-handler"
containerName="service.button-handler"
localIP="172.18.0.7"
networkName="TOASTER"

#stop and remove old container
docker stop $containerName || true && docker rm -f $containerName || true

#remove old image
docker image rm $imageName || true

#build new image
docker build . -t $imageName \
--build-arg TOKEN=$TOKEN \
--build-arg GROUPID=$GROUPID \
--build-arg SQL_HOST=$SQL_HOST \
--build-arg SQL_PORT=$SQL_PORT \
--build-arg SQL_USER=$SQL_USER \
--build-arg SQL_PSWD=$SQL_PSWD

#run container
docker run -d \
--name $containerName \
--restart always \
$imageName

#network setup
docker network connect --ip $localIP $networkName $containerName

#clear chaches
docker system prune -f
```
