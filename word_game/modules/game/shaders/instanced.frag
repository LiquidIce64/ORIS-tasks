#version 430 core

const vec3 placeholder_color = { 1.0f, 0.0f, 1.0f };
const vec3[] team_colors = {
    { 1.0f, 0.0f, 0.0f },
    { 0.0f, 0.0f, 1.0f },
    { 1.0f, 1.0f, 0.0f },
    { 1.0f, 0.0f, 1.0f },

    { 1.0f, 1.0f, 1.0f },
    { 0.6f, 1.0f, 1.0f },
    { 1.0f, 0.6f, 0.6f }
};

uniform int map_size;

const int atlas_size = 8;
uniform sampler2D texture_atlas;

in vec2 fragTexCoord;
vec2 cellTexCoord;
in float textureID;
in float colorID;

out vec4 fragColor;

bool check_neighbors(float x, float y) {
    float offset = 1.0f / atlas_size / 16;
    return (
        texture2D(texture_atlas, vec2(x + offset, y)).a > 0.0f ||
        texture2D(texture_atlas, vec2(x - offset, y)).a > 0.0f ||
        texture2D(texture_atlas, vec2(x, y + offset)).a > 0.0f ||
        texture2D(texture_atlas, vec2(x, y - offset)).a > 0.0f
    );
}

void main() {
    cellTexCoord = vec2(mod(fragTexCoord.s, 1.0f), mod(fragTexCoord.t, 1.0f));
    int colID = int(abs(colorID));
    bool outline = colorID < 0.0f;
    if (outline) colID -= 1;

    float atlas_x = (cellTexCoord.x + int(mod(textureID, atlas_size))) / atlas_size;
    float atlas_y = 1.0f - (cellTexCoord.y + int(textureID / atlas_size)) / atlas_size;

    vec4 color = texture2D(texture_atlas, vec2(atlas_x, atlas_y));
    if (outline && color.a < 1.0f && check_neighbors(atlas_x, atlas_y)) color = vec4(0.6f, 1.0f, 1.0f, 1.0f);
    else if (color.rgb == placeholder_color) color = vec4(team_colors[colID], color.a);
    fragColor = color;
}
