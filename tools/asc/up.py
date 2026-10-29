import sys, os, glob, time
from asc import *
APPS = {
 'as-shot': dict(ver='1eba803f-416a-4b9c-82e1-41db01ded65e', root='~/Mac-Projects/parallax-content/apps/as-shot/posts/2026-10-28_appstore-v1/output',
   shots=lambda r,l: sorted(glob.glob(f'{r}/ekran-6.9/{l}/*.png')), video=lambda r: f'{r}/preview-886x1920.mp4'),
 'onscript': dict(ver='d6530def-6bf8-4bbb-979c-2392a6ab8b4b', root='~/Mac-Projects/parallax-content/apps/onscript/posts/2026-10-28_appstore-v1/output',
   shots=lambda r,l: sorted(glob.glob(f'{r}/ekranlar/{l}/*.png')), video=lambda r: f'{r}/video/onscript-preview-886x1920.mp4'),
}
def get_or_create_set(kind, loc, dtype):
    coll, rel, attr, typ = ('appScreenshotSets','appScreenshotSet','screenshotDisplayType','appScreenshotSets') if kind=='shot' else ('appPreviewSets','appPreviewSet','previewType','appPreviewSets')
    r=api('GET',f'/v1/appStoreVersionLocalizations/{loc}/{coll}')
    for s in r['data']:
        if s['attributes'][attr]==dtype: return s['id']
    r=api('POST',f'/v1/{coll}',{'data':{'type':typ,'attributes':{attr:dtype},'relationships':{'appStoreVersionLocalization':{'data':{'type':'appStoreVersionLocalizations','id':loc}}}}})
    if '_error' in r: raise Exception(r)
    return r['data']['id']
def up_shot(setid, path):
    data=open(path,'rb').read()
    r=api('POST','/v1/appScreenshots',{'data':{'type':'appScreenshots','attributes':{'fileName':os.path.basename(path),'fileSize':len(data)},'relationships':{'appScreenshotSet':{'data':{'type':'appScreenshotSets','id':setid}}}}})
    if '_error' in r: raise Exception(r)
    sid=r['data']['id']; upload_ops(r['data']['attributes']['uploadOperations'],data)
    r=api('PATCH',f'/v1/appScreenshots/{sid}',{'data':{'type':'appScreenshots','id':sid,'attributes':{'uploaded':True,'sourceFileChecksum':md5(data)}}})
    return sid, r.get('data',{}).get('attributes',{}).get('assetDeliveryState',r)
def up_video(setid, path):
    data=open(path,'rb').read()
    r=api('POST','/v1/appPreviews',{'data':{'type':'appPreviews','attributes':{'fileName':os.path.basename(path),'fileSize':len(data),'mimeType':'video/mp4'},'relationships':{'appPreviewSet':{'data':{'type':'appPreviewSets','id':setid}}}}})
    if '_error' in r: raise Exception(r)
    pid=r['data']['id']; upload_ops(r['data']['attributes']['uploadOperations'],data)
    r=api('PATCH',f'/v1/appPreviews/{pid}',{'data':{'type':'appPreviews','id':pid,'attributes':{'uploaded':True,'sourceFileChecksum':md5(data)}}})
    return pid, r.get('data',{}).get('attributes',{}).get('videoDeliveryState',r)
if __name__=='__main__':
    app=sys.argv[1]; locales=sys.argv[2].split(','); what=sys.argv[3]
    A=APPS[app]; root=os.path.expanduser(A['root'])
    locs={l['attributes']['locale']:l['id'] for l in api('GET',f"/v1/appStoreVersions/{A['ver']}/appStoreVersionLocalizations?limit=50")['data']}
    for lc in locales:
        loc=locs[lc]
        if what in('shots','all'):
            s=get_or_create_set('shot',loc,'APP_IPHONE_67')
            for p in A['shots'](root,lc): print(app,lc,os.path.basename(p),up_shot(s,p),flush=True)
        if what in('video','all'):
            s=get_or_create_set('video',loc,'IPHONE_67')
            print(app,lc,'video',up_video(s,A['video'](root)),flush=True)
