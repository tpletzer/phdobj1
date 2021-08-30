import pickle
import glob
import re


#f1 = open('/nesi/nobackup/uoo03104/ym2summertbr.pkl', 'rb')
#summer_tbr = pickle.load(f1)

#create dict matching ym2summerpost.pkl with keys domyrmo and items list of files# been regridded

ym2files = {}

datadir = glob.glob('/nesi/nobackup/uoo03104/clim_summerregridfinal/*')


for f in datadir:
    m_date = re.match(r'^(\d\d\d\d)(\d\d)(\d\d).*$', f.split('/')[-1].split('_')[-2])
    m_time = re.match(r'^(\w)(\d)(\d\d).*$', f.split('/')[-1].split('_')[-1].split('.')[-2])
    m_domain = re.match(r'^(\w)(\d\d).*$', f.split('/')[-1].split('_')[-3:][0])

    yr = m_date.group(1) #match by year
    mo = m_date.group(2)
    dy = m_date.group(3)
    hr = m_time.group(3) #13-36 only
    dom = m_domain.group(1) + m_domain.group(2) #match with other d03

    ym2files[dom + yr + mo] = ym2files.get(dom + yr + mo, [])
    ym2files[dom + yr + mo].append(f)
    print(f)

ym2f = open('/nesi/nobackup/uoo03104/ym2summerregrid.pkl', 'wb')
pickle.dump(ym2files, ym2f)
ym2f.close()
f1 = open('/nesi/nobackup/uoo03104/ym2summerregrid.pkl', 'rb')
summer_pre = pickle.load(f1)


f2 = open('/nesi/nobackup/uoo03104/ym2summerpost.pkl', 'rb')
summer_post = pickle.load(f2)

summer_all = {**summer_pre, **summer_post} 
allf = open('/nesi/nobackup/uoo03104/ym2summerall.pkl', 'wb') 
pickle.dump(summer_all, allf)                                           
allf.close()


