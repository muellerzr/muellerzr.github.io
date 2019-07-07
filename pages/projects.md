---
layout: default
permalink: /projects.html
---
{% assign posts = site.posts | where:"type", "projects" %}

<ul>
  {% for post in posts %}
   <article class = "post">
   	<h1><a href="{{ post.url }}">{{ post.title }}</a></h1>
   	<div class="entry">
   		<p>{{ post.excerpt }}</p>
   	</div>
   </article>

<a href="{{ post.url }}" class="read-more">Read More</a>
  {% endfor %}
</ul>