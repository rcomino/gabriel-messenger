# Documentation

## Definitions


* **Publication**: A publication is a dataclass that includes all the information necessary to generate an entry on any social network. A publication will be shared by a **receiver service** to n **\*sender services\***.


* **Service**: A service is a utility that allow to manage publications in some way. There are two types of services: “**Receivers**” and “**Senders**”.


    * **Receiver Service**: A service that download information from external resources and generate publications. This publications will be upload in configured queues of **sender services**.


    * **Sender Service**: A service that get publications from his queue and publish to external resource.


* **Task**: Tasks are used to schedule coroutines concurrently. See: [asyncio task](https://docs.python.org/3/library/asyncio-task.html).


    * All services will generate a task to perform his functionality.


    * Other tasks: to manage state of services. Currently only to perform shutdown of all services. See next code:


### class src.app.application.Application(configuration: src.inf.configuration.configuration.Configuration)
Application class. The one in charge of governing all the modules.


#### _clean_shutdown()
Handler that will be activated when app receives a SIGINT signal. This create a task to programming a clean
shutdown.

## Workflow

Each **receiver Service** download data from external resource, create publications with this data and send this publications to each queue configured. One queue, one *Sender Service*. Sender get publications from his queue and send to external resource.

## Develop your own service

### Publication


### class src.ser.common.itf.publication.Publication(publication_id: Union[str, int], title: Optional[str] = None, description: Optional[str] = None, url: Optional[str] = None, timestamp: Optional[datetime.datetime] = None, color: Optional[int] = None, images: List[src.ser.common.value_object.file_value_object.FileValueObject] = <factory>, files: List[src.ser.common.value_object.file_value_object.FileValueObject] = <factory>, author: Optional[src.ser.common.value_object.author_value_object.Author] = None, custom_fields: Optional[Any] = None)
Publication Interface. Is the base to create another dataclass that will be used to share publications between
services.


#### abstract property markdown()
Return human-readable markdown text.


#### abstract property text()
Return human-readable plain text.

### Architecture

You will need to implement your new service with this architecture:

### Classes

#### Interfaces


### class src.ser.common.itf.publication.Publication(publication_id: Union[str, int], title: Optional[str] = None, description: Optional[str] = None, url: Optional[str] = None, timestamp: Optional[datetime.datetime] = None, color: Optional[int] = None, images: List[src.ser.common.value_object.file_value_object.FileValueObject] = <factory>, files: List[src.ser.common.value_object.file_value_object.FileValueObject] = <factory>, author: Optional[src.ser.common.value_object.author_value_object.Author] = None, custom_fields: Optional[Any] = None)
Publication Interface. Is the base to create another dataclass that will be used to share publications between
services.


### class src.ser.common.itf.service.ServiceInterface()
Service interface. This the main interface of receiver interface and sender interface.


### class src.ser.common.itf.receiver.ReceiverInterface()
Receiver Interface. Receiver is a service that download data from web and pass to sender service.


### class src.ser.common.itf.sender.SenderMixin()
Sender Interface. This is required to implement in all sender services.

#### Mixins


### class src.ser.common.service_mixin.ServiceMixin()
Common Service Mixin. This class includes methods that required by senders services and receivers services.


### class src.ser.common.receiver_mixin.ReceiverMixin(logger: logging.Logger, wait_time: int, state_change_queue: asyncio.queues.Queue)
Receiver Common Service Mixin. This mixin include methods required by receivers services.


### class src.ser.common.sender_mixin.SenderMixin()
Sender Common Service Mixin. This mixin include methods required by senders services.
