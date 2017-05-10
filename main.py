from datetime import datetime, timedelta
from query import (
    get_resources_for_application,
    get_metrics,
    get_current_metrics
)
import operator
import re
from view import render


RULES = [
    {
        "type": "threshold",
        "metric": "cpu-usage",
        "value": 45,
        "max_value": 100,
        "child_metric": "docker-cpu-usage.*",
   },
   {
        "type": "threshold",
        "metric": "memory-usage",
        "value": 45,
        "max_value": 100,
        "child_metric": "docker-memory-usage.*",
        "child_max_value": 100,
    }
]


def get_data(context, app_name, resource_ids, resource_names, resource_cores, rule, start, end):
    current = get_current_metrics(context,
                                  resource_ids,
                                  rule['metric'])
    data = []
    for resource_id, point in current.items():
        r = {
            'id': resource_id,
            'name': resource_names[resource_id],
            'label': rule['metric'],
            'value': round(point['value'], 2),
            'unit': point['unit'],
            'max_value': rule['max_value'],
        }
        if point['value'] > rule['value']:
            if rule["metric"] == "memory-usage" and re.match("cmp-[^-]+-es[1-9]", resource_names[resource_id]) or rule["metric"] == "memory-usage" and re.match("cmp-[^-]+-kafka[1-9]", resource_names[resource_id]):
                continue
            
            child_metrics = get_metrics(context,
                                        resource_id,
                                        rule['child_metric'],
                                        start,
                                        end)
            r['children'] = []
            for m in child_metrics:
                child_max_value = rule.get('child_max_value')
                if not child_max_value:
                    child_max_value = 100 * resource_cores[resource_id]

                r['children'].append({
                    'name': r['name'],
                    'label': m['label'],
                    'unit': m['unit'],
                    'value': round(m['values'][-1]['value'], 2),
                    'max_value': child_max_value,
                })

            r['children'] = sorted(r['children'],
                                   key=operator.itemgetter('value'),
                                   reverse=True)[:5]

            data.append(r)

    return data


def get(event, context):
    end = datetime.utcnow()
    start = end - timedelta(minutes=10)
    datasets = []
    
    region = event.get("region", "Core")
    appname = "CMP (%s)" % region
    
    name = re.sub(r'([()])', r'\\\1', appname)
    resources = get_resources_for_application(context, name)
    resource_ids = [r['id'] for r in resources]
    resource_names = {r['id']: r['base']['name'] for r in resources}
    resource_cores = {r['id']: r['details']['server']['cpu_cores']
                      for r in resources}
    
    for rule in RULES:
        data = get_data(context,
                        appname,
                        resource_ids,
                        resource_names,
                        resource_cores,
                        rule,
                        start,
                        end)
        datasets.append({
            'application_name': appname,
            'children': data
        })

    table = render(datasets)
    return {
        "html": table
    }
