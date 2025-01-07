#version 430 core

uniform int map_size;

layout(location=0) in vec2 vertPos;
layout(location=1) in vec2 vertTexCoord;

out vec2 fragTexCoord;

void main() {
    gl_Position = vec4(vertPos / map_size, 0.0, 1.0);
    fragTexCoord = vertTexCoord;
}
