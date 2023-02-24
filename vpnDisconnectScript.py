import asyncio

async def main() :
    #name of the vpn you connect to usually
    host = "xyz"
    
    p =  await asyncio.create_subprocess_shell('/opt/cisco/anyconnect/bin/vpn state '+host,stdout=asyncio.subprocess.PIPE)
    
    while True :
        out =  (await p.stdout.readline()).decode("utf-8")
        if out.find('state') > 0 :
            break
    
    output = ""
    
    if out.find('Connected') > 0 :
        process = await asyncio.create_subprocess_shell('/opt/cisco/anyconnect/bin/vpn disconnect',stdout=asyncio.subprocess.PIPE)
        
        stdout , stderr = await process.communicate()
        stdout = stdout.decode("utf-8")
        if stdout.rfind("VPN>") > 0 and stdout[stdout.rfind('VPN')+3] == '>':
            stdout = stdout[0:stdout.rfind('VPN')]
        stdout = stdout.strip()
        
        if stdout.find('error') > 0 :
            output = stdout[stdout.find('error'):]
        else :
            output = "Disconnected"
    else :
        output = "Nothing to disconnect"
      
    print(output)

asyncio.run(main())