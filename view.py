import jinja2, re
from jinja2 import Template

def get_color(value, max=100, alpha=1.0):
    if value > 2*max:
        value = 2*max
    return "hsla({},50%,50%,{})".format((1 - value/max) * 120, alpha)

def strip_container_name(name):
    p = re.compile('(?:Docker CPU usage CPU #|Docker Memory usage \\[)([^]]+)\\]?')
    m = p.search(name)
    if m != None:
        result = m.group(1)
    else:
        result = name
    print 'strip_container_name %s %s' % (name, result)
    return result

"""Render stuff"""
def render_block(data):
    if len(data["children"]) == 0: return ""
    
    template_str = """
    <div class="application clearfix">
        <div class="application__header">
          <span class="title">{{data.application_name}}</span>
        </div>
        <div class="application__body">
            <div class="treemap">
                {% for item in data['children'] %}
                <div class="application__item" style="background-color: {{get_color(item.value, item.max_value, 0.5)}}">
                    <a class="application_item-link" href="/cmp/resources/#resources/{{item.id}}/performance">
                        <span class="name">{{item.name}}</span>
                        <span class="stats">{{item.label}}: {{item.value}}%</span>
                        <div class="application__children">
                            {% for child in item['children'] %}
                                <div class="application__item-child"  style="background-color: {{get_color(child.value, child.max_value, 1.0)}}">
                                    <div class="application__item-child-name">{{strip_container_name(child.label)}}</div>
                                    <span class="stats">{{child.value}}%</span>
                                </div>
                            {% endfor%}
                        </div>
                    </a>
                </div>
                {% endfor%}
            </div>
        </div>
    </div>
    """
    

    template = e.from_string(template_str);
    return template.render(data=data);

e = jinja2.Environment()
e.globals['get_color'] = get_color
e.globals['render_block'] = render_block
e.globals['strip_container_name'] = strip_container_name

def render_style():
    template_str = """
    <!-- Table of the 10 servers with most CPU -->
    <link type="text/css" rel="stylesheet" href="/static/cmp/style/assets/css/main.css">
    <style>
        .metric_block {
            margin: 5px;
            float: left;
            width: 48%;
        }

        .clearfix:after {
          content: "";
          display: table;
          clear: both;
        }

        .application {
          padding: 5px;
        }

        .application_header {
          width: 100%;
          float: left;
        }

        .application__body {
          width: 100%;
          float: left;
          clear: both;
          padding-top: 10px;
        }

        .application__item {
          float: left;
          clear: both;
          width: 100%;
          padding: 8px;
        }
        .application_item-link {
          color: #fff;
          text-decoration: none;
        }
        .application__item-child {
            margin: 2px;
            width: 31%;
            float: left;
            padding: 4px;
        }

        .application__item-child-name {
            min-width: 96%;
            max-width: 96%;
            white-space: nowrap;
            text-overflow: ellipsis;
            overflow: hidden;
        }
    </style>
    """
    template = e.from_string(template_str);
    return template.render();


def render(datasets):
    data_template = e.from_string("""
                <div class="metric_block">
                    {{ render_block(data) }}
                </div>
            """)
    
    html = ""
    for data in datasets:
        if len(data["children"]) != 0:
            html = html + data_template.render(data=data)
    if html == "":
        html = """
        <div class="metric_block>
            <div class="application clearfix">
                <div class="application__body">
                    <center><img src="http://clipart-finder.com/data/mini/kuba_icon_ok.png" /></center>
                </div>
            </div>
        </div>
        """

    return render_style() + html;


def test_render():
    data = [{
        "application_name": "CMP (Core)",
        "children": [
            {
                "name": "cmp-ct-services2",
                "max_value": 400,
                "children": [
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-services2",
                        "value": 282.69,
                        "label": "Docker CPU usage [ElasticSearch]"
                    },
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-services2",
                        "value": 134.23,
                        "label": "Docker CPU usage [PostgresGovernor]"
                    },
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-services2",
                        "value": 78.01,
                        "label": "Docker CPU usage [Kafka]"
                    },
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-services2",
                        "value": 17.72,
                        "label": "Docker CPU usage [Redis]"
                    },
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-services2",
                        "value": 3.86,
                        "label": "Docker CPU usage [InfluxDB]"
                    }
                ],
                "value": 10.22,
                "label": "cpu-usage",
                "id": "4ba0941f-df88-427b-ac59-6e509154f8b8",
                "unit": "percent"
            },
            {
                "name": "cmp-ct-backup",
                "max_value": 400,
                "children": [],
                "value": 10.2,
                "label": "cpu-usage",
                "id": "e9f9e8eb-48d7-4451-a563-e04a44d1c5b9",
                "unit": "percent"
            },
            {
                "name": "cmp-ct-containers2",
                "max_value": 400,
                "children": [
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-containers2",
                        "value": 67.28,
                        "label": "Docker CPU usage [Glass]"
                    },
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-containers2",
                        "value": 49.84,
                        "label": "Docker CPU usage [Trident]"
                    },
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-containers2",
                        "value": 32.64,
                        "label": "Docker CPU usage [Babel]"
                    },
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-containers2",
                        "value": 31.15,
                        "label": "Docker CPU usage [SparkCustomerApi]"
                    },
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-containers2",
                        "value": 25.67,
                        "label": "Docker CPU usage [InfluxdbAdapter2]"
                    }
                ],
                "value": 22.59,
                "label": "cpu-usage",
                "id": "21bd79e3-cbbf-41f2-94ee-e278da3078b4",
                "unit": "percent"
            },
            {
                "name": "cmp-ct-containers1",
                "max_value": 400,
                "children": [
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-containers1",
                        "value": 150.56,
                        "label": "Docker CPU usage [Petros]"
                    },
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-containers1",
                        "value": 63.25,
                        "label": "Docker CPU usage [Trident]"
                    },
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-containers1",
                        "value": 29.55,
                        "label": "Docker CPU usage [InfluxdbAdapter3]"
                    },
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-containers1",
                        "value": 28.96,
                        "label": "Docker CPU usage [InfluxdbAdapter1]"
                    },
                    {
                        "max_value": 400,
                        "unit": "percent",
                        "name": "cmp-ct-containers1",
                        "value": 18.3,
                        "label": "Docker CPU usage [BabelAsyncTasks]"
                    }
                ],
                "value": 16.76,
                "label": "cpu-usage",
                "id": "4c012732-cd1f-421f-95b5-6a873953a873",
                "unit": "percent"
            }
        ]
    },
    {
        "application_name": "CMP (Core)",
        "children": [
            {
                "name": "cmp-ct-services2",
                "max_value": 100,
                "children": [
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services2",
                        "value": 48.05,
                        "label": "Docker Memory usage [Kafka]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services2",
                        "value": 24.85,
                        "label": "Docker Memory usage [ElasticSearch]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services2",
                        "value": 5.74,
                        "label": "Docker Memory usage [Mongo]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services2",
                        "value": 2.59,
                        "label": "Docker Memory usage [SX]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services2",
                        "value": 2.35,
                        "label": "Docker Memory usage [PostgresGovernor]"
                    }
                ],
                "value": 41.62,
                "label": "memory-usage",
                "id": "4ba0941f-df88-427b-ac59-6e509154f8b8",
                "unit": "percent"
            },
            {
                "name": "cmp-ct-containers2",
                "max_value": 100,
                "children": [
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-containers2",
                        "value": 24.01,
                        "label": "Docker Memory usage [Glass]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-containers2",
                        "value": 6.27,
                        "label": "Docker Memory usage [Babel]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-containers2",
                        "value": 2.48,
                        "label": "Docker Memory usage [BabelAsyncTasks]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-containers2",
                        "value": 2.13,
                        "label": "Docker Memory usage [Petros]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-containers2",
                        "value": 2.08,
                        "label": "Docker Memory usage [Trident]"
                    }
                ],
                "value": 41.94,
                "label": "memory-usage",
                "id": "21bd79e3-cbbf-41f2-94ee-e278da3078b4",
                "unit": "percent"
            },
            {
                "name": "cmp-ct-services3",
                "max_value": 100,
                "children": [
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services3",
                        "value": 46.93,
                        "label": "Docker Memory usage [Kafka]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services3",
                        "value": 32.25,
                        "label": "Docker Memory usage [ElasticSearch]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services3",
                        "value": 5.01,
                        "label": "Docker Memory usage [Mongo]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services3",
                        "value": 2.39,
                        "label": "Docker Memory usage [SX]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services3",
                        "value": 2.01,
                        "label": "Docker Memory usage [InfluxDB]"
                    }
                ],
                "value": 45.37,
                "label": "memory-usage",
                "id": "1a6144fe-4860-4c0b-9679-dc5d1d901db1",
                "unit": "percent"
            },
            {
                "name": "cmp-ct-services1",
                "max_value": 100,
                "children": [
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services1",
                        "value": 51.15,
                        "label": "Docker Memory usage [Kafka]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services1",
                        "value": 27.11,
                        "label": "Docker Memory usage [ElasticSearch]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services1",
                        "value": 4.92,
                        "label": "Docker Memory usage [Mongo]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services1",
                        "value": 2.46,
                        "label": "Docker Memory usage [SX]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-services1",
                        "value": 2.44,
                        "label": "Docker Memory usage [PostgresGovernor]"
                    }
                ],
                "value": 38.67,
                "label": "memory-usage",
                "id": "7e938cef-5bdf-49df-b36b-9aecfa99c1ac",
                "unit": "percent"
            },
            {
                "name": "cmp-ct-containers1",
                "max_value": 100,
                "children": [
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-containers1",
                        "value": 6.2,
                        "label": "Docker Memory usage [Babel]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-containers1",
                        "value": 2.41,
                        "label": "Docker Memory usage [Petros]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-containers1",
                        "value": 2.39,
                        "label": "Docker Memory usage [BabelAsyncTasks]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-containers1",
                        "value": 2.37,
                        "label": "Docker Memory usage [Glass]"
                    },
                    {
                        "max_value": 100,
                        "unit": "percent",
                        "name": "cmp-ct-containers1",
                        "value": 2.04,
                        "label": "Docker Memory usage [Trident]"
                    }
                ],
                "value": 42.4,
                "label": "memory-usage",
                "id": "4c012732-cd1f-421f-95b5-6a873953a873",
                "unit": "percent"
            }
        ]
    }]

    print(data)
    return render(data)



def get(event, context):

    table = test_render()
    return {
        "html": table
    }
    pass
