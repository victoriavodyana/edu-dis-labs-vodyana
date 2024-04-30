# Проєктування бази даних

## BE модель

<center style="
    border-radius:4px;
    border: 1px solid #cfd7e6;
    box-shadow: 0 1px 3px 0 rgba(89,105,129,.05), 0 1px 1px 0 rgba(0,0,0,.025);
    padding: 1em;"
>

@startuml

entity Account
entity Account.username <<TEXT>>
entity Account.password <<TEXT>>

entity Survey
entity Survey.name <<TEXT>>
entity Survey.duration <<TEXT>>
entity Survey.isPaused <<BOOLEAN>>
entity Survey.isNamed <<BOOLEAN>>

entity Question
entity Question.text <<TEXT>>

entity Responce
entity Responce.value <<TEXT>>

entity Link
entity Link.usageLimit
entity Link.responceLimit
entity Link.uses
entity Link.responces
entity Link.path

Account.username --* Account
Account.password --* Account

Survey.name --* Survey
Survey.duration --* Survey
Survey.isPaused --* Survey
Survey.isNamed --* Survey

Link.usageLimit -u-* Link
Link.responceLimit -u-* Link
Link.uses --* Link
Link.responces --* Link
Link.path -u-* Link

Responce.value -u-* Responce

Question.text -u-* Question

Account "1,1" -- "0,*" Survey
Survey "1,1" -- "0,*" Question
Question "1,1" -r- "0,*" Responce
Account "0,1" -r- "0,*" Responce
Link "0,*" -- "1,1" Survey

@enduml

</center>



