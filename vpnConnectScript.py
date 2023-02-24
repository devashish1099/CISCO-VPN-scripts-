import asyncio

async def main() :
    #Name of vpn you want to connect to
    host = "xyz"
    
    p =  await asyncio.create_subprocess_shell('/opt/cisco/anyconnect/bin/vpn state '+host,stdout=asyncio.subprocess.PIPE)
    
    while True :
        out =  (await p.stdout.readline()).decode("utf-8")
        if out.find('state') > 0 :
            break
    
    output = ""
    
    if out.find('Disconnected') > 0 :
        #'abc' is the name of keychain containing your password , make sure the script has access to keychains
        #OR you can comment the next line and directly store the password in pwd variable
        process = await asyncio.create_subprocess_shell("security find-generic-password -w -s 'abc'",stdout=asyncio.subprocess.PIPE)
        
        pwd = (await process.stdout.readline()).decode("utf-8")
        
        process1 = await asyncio.create_subprocess_shell('/opt/cisco/anyconnect/bin/vpn -s connect '+host,stdin=asyncio.subprocess.PIPE,stdout=asyncio.subprocess.PIPE)
        
        process1.stdin.write(("\n"+pwd+"\n").encode("utf-8"))
        process1.stdin.close()
        
        stdout , stderr = await process1.communicate()
        stdout = stdout.decode("utf-8")
        
        if stdout.rfind("VPN>") > 0 and stdout[stdout.rfind('VPN')+3] == '>':
            stdout = stdout[0:stdout.rfind('VPN')]
        
        stdout = stdout.strip()
        if stdout.find('error') > 0 :
            output = stdout[stdout.find('error'):]
        else :
            output = stdout[-9:]
        
    else :
        output = "Already connected"

    print(output)
asyncio.run(main())