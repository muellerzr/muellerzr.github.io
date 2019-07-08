---
layout: default
permalink: /projects.html
---
{% assign posts = site.posts | where:"type", "projects" %}

<ul>
  {% for post in posts %}
   <article class = "post">
   	<h1><a href="{{ post.url }}">{{ post.title }}</a>
   	</h1>

   	<div class="entry">
   		<p>{{ post.excerpt }}</p>
   	</div>

   </article>

<a href="{{ post.url }}" class="read-more">Read More</a>
      <span class="read-time" title="Estimated read time">
  <svg id="i-clock" viewBox="0 0 32 32" width="20" height="20" fill="none" stroke="currentcolor" stroke-linecap="round" 
  stroke-linejoin="round" stroke-width="2"><circle cx="16" cy="16" r="14" /><path d="M16 8 L16 16 20 20" /></svg>       

  {% assign words = post.content | number_of_words %}
  {% if words < 360 %}
    1 min read.
  {% else %}
    {{ words | divided_by:180 }} mins read.
  {% endif %}
</span>
<style>
    svg#i-clock {vertical-align: middle;}
</style>
  {% endfor %}
</ul>