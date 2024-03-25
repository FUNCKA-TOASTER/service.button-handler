# ⚙️ TOASTER.BUTTON-HANDLING-SERVICE

![drt98l](https://github.com/STALCRAFT-FUNCKA/toaster.event-routing-service/assets/76991612/08409484-c9b2-41f3-9b40-8e43614f0661)

Вся документирующая информация продублированна внутри кода на английском языке.<br>
All documenting information is duplicated within the code in English.<br>


## 📄 Информация ##

**TOASTER.BUTTON-HANDLING-SERVICE** - сервис обработки событий, классифицированных как нажатие кнопки. Событие приходит от сервиса фентчинга, после чего обрабатывается. Праллельно производятся необходимые действия внутреннего\внешнего логирования.

### Входные данные:

**ButtonEvent (button_pressed):**

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


Пример события, которое приходит от toaster.event-routing-service сервера на toaster.command-handling-service.

Далее, сервис определяет, какая команда была вызвана, а уже после - исполняет все действия, которые за этой командой сокрыты.


### Дополнительно

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
        

*Дополнительная информация, которая может пригодиться для поднятия сервиса внутри инфраструктуры.
