import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30367;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=txg49604;PWD=krAF2h7MrxBxNuk3",'','')
print(conn)
print("connection successful")

sql="SELECT * FROM USERS"
stmt = ibm_db.exec_immediate(conn,sql)
dictionary = ibm_db.fetch_assoc(stmt)
while dictionary!=False:
    print("Full ROW: ",dictionary)
    dictionary=ibm_db.fetch_assoc(stmt)