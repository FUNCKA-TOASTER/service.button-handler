# ⚙️ TOASTER.BUTTON-HANDLING-SERVICE

![main_img](https://github.com/STALCRAFT-FUNCKA/toaster.button-handling-service/assets/76991612/40e1cb24-f2d0-4786-bf49-a8dabe0f35b2)

## 📄 Информация ##

**TOASTER.BUTTON-HANDLING-SERVICE** - сервис обработки событий, классифицированных как нажатие кнопки. Событие приходит от сервиса фетчинга, после чего обрабатывается. Праллельно производятся необходимые действия внутреннего\внешнего логирования.

### Входные данные:

**ButtonEvent (button_pressed):**
```
content type: application\json

{
    "ts": 1709107935, 
    "datetime": "2024-02-28 11:12:15", 
    "event_type": "button_pressed", 
    "event_id": "e93488a3813b59f6c6b53ee51f59103e2a9240d6", 
    "user_id": 206295116, 
    "user_name": "Руслан Башинский", 
    "user_nick": "oidaho", 
    "peer_id": 2000000002, 
    "peer_name": "FUNCKA | DEV | CHAT", 
    "chat_id": 2, 
    "cmid": 2618, 
    "button_event_id": "ac89a3425ec3", 
    "payload": {
        "keyboard_owner_id": 206295116, 
        "call_action": "test"
    }
}
```

Пример события, которое приходит от toaster.event-routing-service сервера на toaster.button-handling-service.

Далее, сервис определяет, какая команда была вызвана, а уже после - исполняет все действия, которые за этой командой сокрыты.


### Дополнительно

Docker setup:
```
    docker network
        name: TOASTER
        ip_gateway: 172.18.0.1
        subnet: 172.18.0.0/16
        driver: bridge
    

    docker image
        name: toaster.button-handling-service
        args:
            TOKEN: "..."
            GROUPID: "..."
            SQL_HOST: "..."
            SQL_PORT: "..."
            SQL_USER: "..."
            SQL_PSWD: "..."
    

    docker container
        name: toaster.button-handling-service
        network_ip: 172.1.08.7

    docker volumes:
        /var/log/TOASTER/toaster.button-handling-service:/service/logs
```

Jenkisn shell command:
```
imageName="toaster.button-handling-service"
containerName="toaster.button-handling-service"
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
--volume /var/log/TOASTER/$imageName:/service/logs \
--restart always \
$imageName

#network setup
docker network connect --ip $localIP $networkName $containerName

#clear chaches
docker system prune -f
```
