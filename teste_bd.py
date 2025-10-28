from database import executar_comandos
print(executar_comandos("SELECT DATABASE();", fetchone=True))
