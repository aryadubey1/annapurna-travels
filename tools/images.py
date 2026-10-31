import sys,os
from PIL import Image
dl,out=sys.argv[1],sys.argv[2]
M={ # name: source
'hero-sunset':'2419_IMG_7312.jpg','yard-sunset':'2423_IMG_7310.jpg','bus-side':'2813_IMG_7674.JPG',
'yard-row':'2838_IMG_7668.JPG','yard-row2':'2840_IMG_7669.JPG','garage':'2903_IMG_7670.JPG','office':'2904_IMG_7673.JPG',
'founder-1989':'2842_IMG_7691.JPG','bus-red':'3103_IMG_7814.JPG','interior-blue':'3157_IMG_7821.JPG',
'coach-road':'3425_IMG_20190603_054539970.jpg','interior-fabric':'3429_IMG_20210813_192318.jpg','interior-fabric2':'3430_IMG_20210813_192420.jpg',
'coach-41':'3520_IMG20200411090225.jpg','coach-blue':'3523_IMG20200411090047.jpg','interior-leather':'3647_IMG_20210813_193332.jpg',
'fleet-line':'3680_IMG_20200309_122131.jpg','interior-purple':'3728_DSC08687.JPG','coach-orange':'3761_PHOTO-2023-07-27-09-57-50.jpg',
'coach-49':'3763_PHOTO-2023-07-27-09-57-39.jpg','coach-45':'3851_IMG-20190227-WA0067.jpg','coach-pair':'3852_IMG-20190227-WA0072.jpg',
'coach-dawn':'3855_IMG20200321065859.jpg','coach-51':'4170_IMG_7307.jpg','coach-50':'11020_ChatGPT_Image_Aug_31__2025__04_13_52_PM.png',
'group':'318_turn_05.jpg',
'dest-ujjain':'2656_mahakal_mandir-ujjain-madhya-pradesh-hero.jpeg','dest-bandhavgarh':'2659_bandhavgarh-national-park.jpg',
'dest-mandu':'2707_jahaz-mahal-mandu.jpg','dest-indore':'2708_Indore_Rajwada01.jpg','dest-bhopal':'2718_cq5dam.web.1280.1280.jpeg',
'dest-kanha':'2726_bandhavgarh-vs-kanha.webp','dest-lake':'3910_lake.png',
'car-dzire':'3280_Dzire_Tour.jpg','car-innova':'3282_unmatched-design1600x1000.jpg','car-bolero':'3283_Mahindra_Bolero_Neo_1_1626164445826_1629607070175.jpg',
'car-tavera':'3284_Chevrolet-Tavera-Right-Front-Three-Quarter-49908_ol.webp','car-audi':'3286_l153_13151567429550.webp',
'car-fortuner':'3288_Fortuner-bronze.webp','car-scorpio':'3294_hqdefault.webp',
}
for n,s in M.items():
  im=Image.open(os.path.join(dl,s)).convert('RGB')
  for w,suf in ((1600,''),(800,'-sm')):
    c=im.copy(); c.thumbnail((w,w*2)); c.save(f'{out}/{n}{suf}.webp','WEBP',quality=78,method=6)
# logo
lg=Image.open(os.path.join(dl,'281_Annapurna_Logo_page-0001-removebg-preview.png')).convert('RGBA'); lg=lg.crop(lg.getbbox()); lg.save(f'{out}/logo.png',optimize=True); lg.save(f'{out}/logo.webp','WEBP',quality=90)
# clients
C=['396_Dilip_Buildcon_Limited_Logo-removebg-preview.png','373_Screenshot_2025-02-26_at_2.18.39_PM-removebg-preview.png','344_crompton-greaves-758x379-removebg-preview.png','351_images.png','356_185303-aristo-logo.webp','334_e1fe2334a159f143d827fb964219a454237bfb8dca568852113713164f767d50.webp','393_logo__1_.png','389_CoreCard_Corporation_logo.png','368_images__2_-removebg-preview.png','336_unnamed.png','367_images__1_-removebg-preview__1_.png','323_mp-tourism-logo-0663C0C066-seeklogo.com.png','364_images-removebg-preview.png','332_Procter___Gamble_logo.svg.png','388_481192182_1148055457019650_263120329413963574_n-removebg-preview.png','375_final-logo-of-rs-e1694845390978.png','374_Screenshot_2025-02-26_at_2.22.22_PM-removebg-preview.png','362_images__1_-removebg-preview.png','371_images__2_-removebg-preview__1_.png','350_292459508_554352759728576_1363922852233029101_n-removebg-preview.png','416_images-removebg-preview__1_.png','421_images.png','415_550-5501196_trident-group-corporate-company-logo-png-transparent-png-removebg-preview.png','378_logonew1-1-removebg-preview.png','419_SET_India_2016.webp','345_sintex-logo-B16804CE0C-seeklogo.com.png']
for i,s in enumerate(C):
  im=Image.open(os.path.join(dl,s)).convert('RGBA'); bb=im.getbbox(); im=im.crop(bb) if bb else im
  im.thumbnail((360,200)); im.save(f'{out}/clients/c{i+1:02d}.webp','WEBP',quality=88)
print('ok')
