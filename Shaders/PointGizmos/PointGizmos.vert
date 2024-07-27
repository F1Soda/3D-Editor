#version 330 core

layout (location = 0) in vec3 in_color;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;
uniform vec3 position;

out vec3 color;

void main() {
    color = in_color;
    vec4 pos = m_proj * m_view * m_model * (vec4(position, 1.0));
    gl_Position = pos;
}