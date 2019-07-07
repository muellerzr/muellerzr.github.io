---
layout: default
permalink: /projects.html
---
{% assign posts = site.posts | where:"type", "projects" %}

<ul>
{% for post in posts %}
<li>
<a href="{{ site.url }}{{site.baseurl}}{{ post.url }}">{{ post.title }}</a>
</li>
{% endfor %}
<ul>