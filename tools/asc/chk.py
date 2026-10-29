from asc import *
for app,ver in [('as-shot','1eba803f-416a-4b9c-82e1-41db01ded65e'),('onscript','d6530def-6bf8-4bbb-979c-2392a6ab8b4b')]:
    for l in api('GET',f'/v1/appStoreVersions/{ver}/appStoreVersionLocalizations?limit=50')['data']:
        for s in api('GET',f"/v1/appStoreVersionLocalizations/{l['id']}/appPreviewSets")['data']:
            for p in api('GET',f"/v1/appPreviewSets/{s['id']}/appPreviews")['data']:
                print(app,l['attributes']['locale'],'video',p['attributes']['videoDeliveryState']['state'])
        for s in api('GET',f"/v1/appStoreVersionLocalizations/{l['id']}/appScreenshotSets")['data']:
            st=[x['attributes']['assetDeliveryState']['state'] for x in api('GET',f"/v1/appScreenshotSets/{s['id']}/appScreenshots")['data']]
            print(app,l['attributes']['locale'],'shots',len(st),set(st))
