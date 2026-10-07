"""Find duplicate and missing OpenAPI operation identifiers."""
import argparse,csv,io,json,math,re
from collections import Counter
from datetime import date,datetime
from pathlib import Path

def analyze(data):
    ids=[];missing=[]
    for path,item in data.get('paths',{}).items():
        for method,operation in item.items():
            if method not in {'get','post','put','patch','delete','head','options','trace'}:continue
            if operation.get('operationId'):ids.append(operation['operationId'])
            else:missing.append(method.upper()+' '+path)
    return {'duplicates':sorted(name for name,n in Counter(ids).items() if n>1),'missing':sorted(missing)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path,help='UTF-8 JSON input file')
    parser.add_argument('--explain',action='store_true',help='Send the local report to the configured chat gateway')
    args=parser.parse_args()
    report=analyze(json.loads(args.input.read_text(encoding='utf-8')))
    if args.explain:
        from gateway_client import explain
        print(explain(report))
    else:print(json.dumps(report,ensure_ascii=False,indent=2))
