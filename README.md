# WebApp Influjobs
Proyecto de final de curso para 4Geeks Academy

## Descripción
Este proyecto es una plataforma para poner en contacto a Influencer y Empresas, para relaciones estrictamente laborales. Tanto el usuario empresa como el influencer pueden crear un perfil y rellenarlo con sus datos. Está habilitado que el usuario Empresa pueda crear ofertas de trabajo, en las que el usuario Influencer podrá inscribirse. 
Se hace seguimiento del estado de la candidatura y aparecen avisos para ambos usuarios cuando hay novedades. 

Para unas futuras versiones se quiere habilitar un sistema de comunicación entre los dos tipos de usuarios, así como agendar reuniones.

## Instalación
Se debe hacer
```<pipenv run start>```
pero si tocamos los modelos habrá que hacer también un
```<pipenv run migrate>```
```<pipenv run upgrade>```

Para crear la base de datos recomendamos hacer un restart de la base de datos para empezar de 0:
```<pipenv run reset_db>```

Activaremos el puerto de Front-End con
```<npm run start>```

## Uso
Una vez instalado, puedes crear un usuario para ver sus funcionalidades. El usuario Empresa da un poco más de juego, de momento, ya que hay gestión de candidatos que se aceptan o se rechazan, a parte de la creación de ofertas de trabajo distintas. Puedes navegar por toda la página y crear lo que necesites.

## Tecnologías
Para este proyecto se ha usado HTML, Bootstrap, React Js, SQL Alchemy y Python. 

## Contacto
Pueden ponerse en contacto conmigo usando el correo paufargasroca@gmail.com o contactando con Michael Aprile y Merlina Dowgaluk.

## Estado del proyecto
Este proyecto es la culminación del Bootcamp de Full-Stack Developer de 4 Geeks. Aunque su estado es presentado y aprobado, siempre hay margen de mejora, sobretodo en funcionalidades que podemos añadir.
