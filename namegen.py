import random

name_start1 = ['Aba','Abde','Abre','Aby','Aca','Acle','Acri','Acro','Adme','Adra','Aea','Aegi','Aei','Aeo','Aese','Aeto','Aga','Age','Agi','Agri','Aia','Aka','Akti','Ala','Alco','Ale','Alka','Alki','Alo','Alphi','Ama','Ame','Ami','Amphi','Ana','Anchi','Andro','Ane','Anta','Anthe','Anti','Ape','Aphi','Apo','Arca','Arche','Arci','Arga','Ari','Arra','Arte','Asca','Asta','Asty','Atro','Atta','Aute','Bace','Bae','Bali','Bio','Boe','Bria','Care','Carpo','Casto','Cea','Cebri','Cele','Cephi','Chae','Chare','Chari','Choe','Chromi','Chryso','Cine','Cisse','Clea','Cleo','Clyto','Cnoe','Coe','Cordy','Cory','Crati','Creti','Croe','Ctea','Cyre','Dae','Dami','Damo','Dana','Daphi','Davo','Dei','Dema','Demo','Deo','Derky','Dexi','Dia','Dio','Dithy','Dore','Dori','Doro','Drya','Dymno','Eche','Eio','Ela','Elpe','Empe','Endy','Enge','Epa','Epe','Ephi','Era','Ere','Ergi','Erxa','Euca','Euche','Eudo','Eue','Euge','Euma','Eune','Eury','Euthy','Eva','Eve','Fae','Gale','Gany','Gaua','Genna','Gera','Glau','Gorgo','Gyra','Hae','Hagi','Hali','Harma','Harmo','Harpa','Hege','Heira','Heiro','Helge','Heli','Hera','Hermo','Hiero','Hippo','Hya','Hype','Hyrca','Iatro','Iby','Ica','Ido','Illy','Ina','Iphi','Iro','Isa','Isma','Iso','Ithe','Kae','Kale','Kalli','Kame','Kapa','Kari','Karo','Kau','Keo','Kera','Kleo','Krini','Krito','Labo','Lae','Lama','Lamu','Lao','Laso','Lea','Lei','Leo','Linu','Luko','Lyca','Lyco','Lysa','Lysi','Maca','Macha','Mae','Maia','Maka','Male','Mante','Marci','Marsy','Mega','Megi','Mela','Mele','Metho','Midy','Mise','Mono','Morsi','Myrsi','Naste','Nausi','Nea','Nele','Neri','Nica','Nico','Nire','Nomi','Nycti','Oche','Ocho','Oea','Oene','Oeno','Oile','Ona','One','Ophe','Ori','Orsi','Ory','Pae','Pala','Pana','Pandi','Pani','Panta','Para','Pata','Peiri','Pele','Peli','Peri','Phae','Phala','Philo','Phyla','Poe','Poly','Praxi','Prota','Pryta','Saby','Saty','Scama','Scytha','Sele','Sila','Simo','Sisy','Sopho','Stesa','Sya','Sylo','Syne','Tala','Teba','Tele','Tene','Theo','Therse','Thrasy','Tima','Tiry','Trio','Xanthi','Xena','Xeno'];

name_starts = [name_start1]

name_end1 = ['ndros','bios','bulos','chus','cles','cydes','damos','dides','don','doros','dotus','gnis','goras','kles','kos','krates','laktos','laus','leon','llias','llos','llus','machos','machus','menes','menos','mos','ndius','nes','neus','nidas','nides','nos','nthius','patros','phanes','phantes','phimus','phnus','phon','phoros','phorus','phus','pides','pompos','pompus','pon','ppos','rax','reas','rides','ros','sias','sides','sius','stius','stor','stos','stus','talos','thenes','theus','tios'];

name_end2 = ['ndria','boea','casta','caste','cheia','chis','cleia','dee','deia','dike','dina','doce','dora','dusa','gaea','kia','laia','lea','line','llis','lope','mache','mathe','meda','mede','meia','mela','mene','mere','mia','mina','mpias','ndra','ne','neira','nessa','nia','nice','niera','nike','nippe','nna','nome','nope','nta','nthia','pe','phae','phana','phane','phile','phobe','phone','pia','polis','pris','pyle','reia','rine','ris','rista','rpia','sia','ssa','steia','stis','syne','ta','tea','thea','theia','thia','thippe','thra','thusa','thyia','tis','trite'];

name_ends = [name_end1, name_end2]

def gen_name():
	name = random.choice(random.choice(name_starts))
	name += random.choice(random.choice(name_ends))
	return name

if __name__ == '__main__':
	for x in range(100):
		print(gen_name())
