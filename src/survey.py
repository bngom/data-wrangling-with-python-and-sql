import pandas.io.sql
import os


def generatelastsurveystructure(connexion: object):
    """generate the last last known survey structure in a csv file
    :arg
        an instance of the class DBConnection"""
    lastsurveystructure = str("""SELECT * FROM SurveyStructure""")
    lastsurveystructure = pandas.io.sql.read_sql(lastsurveystructure, connexion)
    PATH = ".\src\db"
    lastsurveystructure.to_csv(path_or_buf=os.path.join(PATH, "lastsurveystructure.csv"), sep=",", header=True,
                               index=None)


def getlastsurveystructure():
    """Get the last known survey structure"""
    filename = os.path.join(".\src\db", "lastsurveystructure.csv")
    try:
        lastsurveystructure = pandas.read_csv(filename, sep=",", index_col=False)
    except IOError as e:
        raise(f"No such file or directory {filename}")
    return lastsurveystructure


def createallsurveydataview(connector, dynamic_sql_survey_data):
    """Create the view vw_AllSurveyData"""
    connector.execute_query(dynamic_sql_survey_data)


def getdynamicsurveydata(connexion: object):
    strQueryTemplateForOuterUnionQuery = str("""SELECT UserId,                     
        <SURVEY_ID> as SurveyId,           
        <DYNAMIC_QUESTION_ANSWERS>       
        FROM [User] as u                  
        WHERE EXISTS                     
        (                                
        SELECT * FROM Answer as a    
        WHERE u.UserId = a.UserId   
        AND a.SurveyId = <SURVEY_ID>  
        )""")

    strQueryTemplateForAnswerQuery = str("""COALESCE(
         (
           SELECT a.Answer_Value
           FROM Answer as a
           WHERE  a.UserId = u.UserId
           AND a.SurveyId = <SURVEY_ID>
           AND a.QuestionId = <QUESTION_ID>
         ), 
         -1) AS ANS_Q<QUESTION_ID>""")

    strQueryTemplateForNullColumn = " NULL AS ANS_Q<QUESTION_ID>"

    strCurrentUnionQueryBlock = ""

    strFinalQuery = ""

    strSurveyCursorQuery = " SELECT SurveyId FROM Survey ORDER BY SurveyId "

    surveyCursor = pandas.io.sql.read_sql(strSurveyCursorQuery, connexion)
    for idx, _row in surveyCursor.iterrows():

        strCurrentQuestionCursor = str("""SELECT * 
        FROM 
            (
                SELECT SurveyId,  QuestionId, 1 as InSurvey
                FROM SurveyStructure
                WHERE SurveyId = {0}
                UNION 
                SELECT {0} as SurveyId, 
                    Q.QuestionId, 
                    0 as InSurvey 
                FROM 
                    Question as Q 
                WHERE NOT EXISTS ( 
                    SELECT * 
                    FROM SurveyStructure as S 
                    WHERE S.SurveyId = {0} AND S.QuestionId = Q.QuestionId 
                ) 
            ) as t ORDER BY QuestionId""").format(str(_row["SurveyId"]))

        currentQuestionCursor = pandas.io.sql.read_sql(strCurrentQuestionCursor, connexion)

        strColumnsQueryPart = ""

        for index, row in currentQuestionCursor.iterrows():

            if int(row["InSurvey"]) == 0:

                strColumnsQueryPart = strColumnsQueryPart + strQueryTemplateForNullColumn.replace("<QUESTION_ID>", str(row["QuestionId"]))

            else:
                strColumnsQueryPart = strColumnsQueryPart + strQueryTemplateForAnswerQuery.replace("<QUESTION_ID>", str(row["QuestionId"]))

            if index != currentQuestionCursor.index[-1]:
                # This is the NOT last iteration
                strColumnsQueryPart = strColumnsQueryPart + ", "
                #pass
        strCurrentUnionQueryBlock = strQueryTemplateForOuterUnionQuery.replace("<DYNAMIC_QUESTION_ANSWERS>", strColumnsQueryPart)

        strCurrentUnionQueryBlock = strCurrentUnionQueryBlock.replace("<SURVEY_ID>", str(_row["SurveyId"]))

        strFinalQuery = strFinalQuery + strCurrentUnionQueryBlock

        if idx != surveyCursor.index[-1]:
            # This is NOT the last iteration
            strFinalQuery = strFinalQuery + ' UNION '

    strDynamicSQLSurveyData = str("""CREATE OR ALTER VIEW vw_AllSurveyData AS""")

    strDynamicSQLSurveyData = strDynamicSQLSurveyData + " ( " + strFinalQuery + " )"

    return strDynamicSQLSurveyData





