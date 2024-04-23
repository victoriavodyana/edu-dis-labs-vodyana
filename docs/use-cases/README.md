# Модель прецедентів

## Загальна схема

<center style="
    border-radius: 4px;
    border: 1px solid #cfd7e6;
    box-shadow: 0 1px 3px 0 rgba(89,105,129,.05), 0 1px 1px 0 rgba(0,0,0,.025);
    padding: 1em;
">

@startuml

    :Гість: as Guest
    :Зареєстрований користувач: as AuthorisedUser

    ("<b>ACCOUNT.CREATE</b>\nСтворити обліковий запис") as CreateAccount
    ("<b>ACCOUNT.DELETE</b>\nВидалити обліковий запис") as DeleteAccount
    ("<b>ACCOUNT.MODIFY</b>\nЗмінити властивості облікового запису") as ModifyAccount
    ("<b>USER.CREATE_SURVEY</b>\nСтворити опитування") as CreateSurvey
    ("<b>USER.DELETE_SURVEY</b>\nВидалити опитування") as DeleteSurvey
    ("<b>USER.GET_SURVEY_RESULT</b>\nПереглянути відповіді на опитування") as GetSurveyResult
    ("<b>USER.LOGIN</b>\nПройти ідентифікацію в системі") as LogIn
    ("<b>USER.LOGOUT</b>\nСкинути дані про ідентифікацію в системі") as LogOut
    ("<b>USER.MODIFY_SURVEY</b>\nРедагувати опитування") as ModifySurvey
    ("<b>USER.STAT_SURVEY</b>\nПереглянути властивості опитування") as StatSurvey
    ("<b>USER.TAKE_ANON_SURVEY</b>\nПройти анонімне опитування") as TakeAnonSurvey
    ("<b>USER.TAKE_NAMED_SURVEY</b>\nПройти поіменне опитування") as TakeNamedSurvey

    Guest -u-> CreateAccount
    Guest --> LogIn
    Guest -r-> TakeAnonSurvey

    AuthorisedUser -r-> ModifyAccount
    AuthorisedUser -u-> DeleteAccount
    AuthorisedUser -u-> LogOut
    AuthorisedUser --> CreateSurvey
    AuthorisedUser -u-> DeleteSurvey
    AuthorisedUser --> StatSurvey
    AuthorisedUser --> ModifySurvey
    AuthorisedUser --> GetSurveyResult
    AuthorisedUser -l-> TakeAnonSurvey
    AuthorisedUser -d-> TakeNamedSurvey

@enduml

</center>