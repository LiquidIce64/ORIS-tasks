#version 430 core

uniform int map_size;

layout(std430, binding=3) buffer instances
{
    vec4 instance_data[];
};

layout(location=2) in vec2 vertPos;
layout(location=3) in vec2 vertTexCoord;

out vec2 fragTexCoord;
out float textureID;
out float colorID;

void main() {
    vec4 data = instance_data[gl_InstanceID];
    gl_Position = vec4((vertPos + data.xy * 2 + vec2(1.0f)) / map_size - vec2(1.0f), 0.0, 1.0);
    fragTexCoord = vertTexCoord;
    textureID = data.z;
    colorID = data.w;
}
