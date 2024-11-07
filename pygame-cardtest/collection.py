class Collection:
    def __init__(self,name,location,file_name,discovery_status):
        self.name = name
        self.location = location
        self.file_name = file_name
        self.discovery_status = discovery_status
class Storage:
    def __init__(self):
        self.character_list = [
            Collection("Kazuma",(),"card/Kazuma.jpg",False),
            Collection("Shubaru yamato",(),"card/Shubaru yamato.jpg",False),
            Collection("Rin shirozaki",(),"card/Rin shirozaki.jpg",False),
            Collection("Shizuo Valkyria",(),"card/Shizuo Valkyria.jpg",False),
            Collection("Marry Eternalblood",(),"card/Marry Eternalblood.jpg",False),
            Collection("Traisy o' Reapper",(),"card/Traisy o' Reapper.jpg",False),
            Collection("Kaguya Hime",(),"card/Kaguya Hime.jpg",False),
            Collection("Gaia Theyggdrasill",(),"card/Gaia Theyggdrasill.jpg",False),
            Collection("Himego Kanade",(),"card/Himego Kanade.jpg",False),
            Collection("Hibaki yamanashi",(),"card/Hibaki yamanashi.jpg",False),
            Collection("Jibrili",(),"card/Jibrili.jpg",False),
            Collection("Isuna",(),"card/Isuna.jpg",False),
            Collection("Hikari",(),"card/Hikari.jpg",False),
            Collection("Hibani",(),"card/Hibani.jpg",False)]
class check_discovery:
    def check(self):
        storage = Storage()
        f = open("demofile.txt", "r") #เปลี่ยนชื่อfileให้ตรงด้วยล่ะ
        for i in f:
            for j in range(14):
                if i.strip() == storage.character_list[j].name:
                    storage.character_list[j].discovery_status = True
