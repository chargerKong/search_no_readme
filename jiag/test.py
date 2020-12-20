#!/usr/bin/env python
# coding=utf-8
import requests
import re
import json

def group_to_id(groups): 
    """
    return a dict. keys mean group name, values mean group id
    """
    url = "https://gitlab.com/"
    ans = {}
    # headers = {
    #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #     "accept-encoding": "gzip, deflate, br",
    #     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,eo;q=0.7",
    #     "cache-control": "max-age=0",
    #     "cookie": "__cfduid=d282223af57df9e508388d68c784f27651606450354; experimentation_subject_id=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkltVmlZVEZsWmpGaUxUWmtaamd0TkRWak1DMWhNekU0TFRnek1ERTNZalk0TmpsbU5pST0iLCJleHAiOm51bGwsInB1ciI6ImNvb2tpZS5leHBlcmltZW50YXRpb25fc3ViamVjdF9pZCJ9fQ%3D%3D--17490a42c09fe5141e4f4a8ea3a4dc12efd5aefe; sidebar_collapsed=false; _ga=GA1.2.684008967.1608117460; _biz_uid=2cf23f130753428b8bba902b69d31871; _mkto_trk=id:194-VVC-221&token:_mch-gitlab.com-1608117461182-93039; _fbp=fb.1.1608117461408.548806448; _hjid=32f7e4cb-080e-4f78-96a4-71e2197fe7b2; _gcl_au=1.1.888157610.1608117780; vid=e27618d7-2e3b-4a7e-9b42-0df0f76f3fdf; _uetvid=0e3850c03f9111ebb87d4fd4d12fe097; _biz_flagsA=%7B%22Version%22%3A1%2C%22XDomain%22%3A%221%22%2C%22ViewThrough%22%3A%221%22%2C%22Mkto%22%3A%221%22%7D; cf_clearance=7f996f516939da6c41c7fb4d071d50679292f4d4-1608202702-0-150; known_sign_in=djlpb3I3dDR6cGpTK2V5S2dvU3Rta3ZjVzZ4WkFUNGZIQUJLMDAvV2ZwSlZtMTdXQ3grNTRoQldxVGVmNllkV2lFcWtiU09qRm81MmliWFBsYTFDSk1oVDhOSDBNbERndHJXUXdJMnV1Ykt0Yzd6eHVNN29JallkemxlSjlUQW5DVmQra1VKS3BWMlZoK00vNVJMU3p3PT0tLVRNU3BHRkJMOS9hbUErbDRwa2p5aGc9PQ%3D%3D--573a8ae33fac794741eff6b8acf2b2e792c7a7ed; _biz_nA=20; _biz_pendingA=%5B%5D; _sp_ses.6b85=*; _sp_id.6b85=0411f3da-dad0-469c-9197-573992991d17.1606450359.8.1608456536.1608452243.c94398d0-e05c-4f13-8918-881f9f4378a0; _gitlab_session=c6a72fa1b6079a6f2a96048636d386ce",
    #     "sec-ch-ua": 'Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-fetch-dest": "document",
    #     "sec-fetch-mode": "navigate",
    #     "sec-fetch-site": "none",
    #     "sec-fetch-user": "?1",
    #     "upgrade-insecure-requests": "1",
    #     "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    # }
    for group in groups:
        try:
            res = requests.get(url + group, headers=None)
            ans[group] = re.findall("Group ID: (\d+)", res.text)[0]
        except Exception as e:
            print(e)
    return ans


def getAllSubGroup(name2id):
    """
    input:dict, {name: id}
    output: {name: {id:123, subgroup:{}}},
            [name1, name2, name3] elements represent the projects which do not have readme 
    """
    ans = {} # store subgroup
    noreadme = []
    for name, id in name2id.items():
        subgroup_url = "https://gitlab.com/api/v4/groups/" + str(id) + "/subgroups?public_token=gJ58pqci-xkdA2uJhcis"
        print("finding " + name + " subgroup")
        res_group = json.loads(requests.get(subgroup_url).text)
        ans.update({name: {"id": id, "project":None, "subgroup": None}})
        print(name + "'s subgroup has " + str(len(res_group)) + " groups")
        
        project_url = "https://gitlab.com/api/v4/groups/" + str(id) + "/projects?public_token=gJ58pqci-xkdA2uJhcis"
        print("finding " + name + " projects")
        res_pro = json.loads(requests.get(project_url).text)
        # import pdb
        # pdb.set_trace()
        #######
        print(name + " has " + str(len(res_pro)) + " projects")
        if len(res_group) > 0:
            for subgroup in res_group:
                ans[name]["subgroup"] = getAllSubGroup({subgroup["name"]: subgroup["id"]})
        if len(res_pro) > 0:
            for pro in res_pro:
                ans[name]["project"] = {
                    "name": pro["name"],
                    "id": pro["id"],
                    "has_readme": (not pro["readme_url"] is None)
                }
                if not ans[name]["project"]["has_readme"]:
                    noreadme.append(pro['name'])

    return ans, noreadme



#name2id = group_to_id(["klqgroup"])
#print(name2id)
sub = getAllSubGroup({'klqgroup':'10420289'})
print(sub)
