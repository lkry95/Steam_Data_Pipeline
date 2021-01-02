import webscrapeData
import dataCleaning
import uploadMySQL
import executeMySQLScripts
import createLukesPicksTxt
import sendEmail


webscrapeData.get_data()
dataCleaning.clean_data()
uploadMySQL.upload_MySQL()
executeMySQLScripts.executeScripts()
createLukesPicksTxt.create_Lukes_Picks()
sendEmail.send_email()