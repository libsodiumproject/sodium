def seconds(seconds: int):
    import datetime as dt
    from datetime import datetime
    return int((datetime.now() + dt.timedelta(seconds=seconds) - datetime(1970, 1, 1)).total_seconds())

def render(templatename: str, **kwargs):
    from jinja2 import Template
    t = Template(open(f"src/templates/{templatename}").read())
    return t.render(**kwargs)
