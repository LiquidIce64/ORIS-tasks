#version 430 core

const vec3[] team_colors = {
    { 1.0f, 0.0f, 0.0f },
    { 0.0f, 0.0f, 1.0f },
    { 1.0f, 1.0f, 0.0f },
    { 1.0f, 0.0f, 1.0f }
};
uniform int map_size;

layout(std430, binding=2) buffer map_data
{
    int owner[];
};

uniform sampler2D texture;
in vec2 fragTexCoord;
vec2 cellTexCoord;

out vec4 fragColor;

int calculateBorder() {
    int current_x = int(fragTexCoord.s);
    int current_y = int(fragTexCoord.t);
    int current_i = map_size * current_y + current_x;
    int current_owner = owner[current_i];

    bool down = cellTexCoord.y <= 0.125f && current_y > 0;
    bool up = cellTexCoord.y >= 0.875f && current_y + 1 < map_size;
    bool left = cellTexCoord.x <= 0.125f && current_x > 0;
    bool right = cellTexCoord.x >= 0.875f && current_x + 1 < map_size;

    // Edges
    if (down  && owner[current_i - map_size] != current_owner) return current_owner;
    if (up    && owner[current_i + map_size] != current_owner) return current_owner;
    if (left  && owner[current_i - 1] != current_owner) return current_owner;
    if (right && owner[current_i + 1] != current_owner) return current_owner;

    // Corners
    if (down && left  && owner[current_i - map_size - 1] != current_owner) return current_owner;
    if (down && right && owner[current_i - map_size + 1] != current_owner) return current_owner;
    if (up   && left  && owner[current_i + map_size - 1] != current_owner) return current_owner;
    if (up   && right && owner[current_i + map_size + 1] != current_owner) return current_owner;

    return 0;
}

void main() {
    cellTexCoord = vec2(mod(fragTexCoord.s, 1.0f), mod(fragTexCoord.t, 1.0f));

    bool grid_mask = mod(floor(fragTexCoord.s) + floor(fragTexCoord.t), 2.0f) == 0.0f;

    vec2 edge_mask_vec = abs(cellTexCoord - 0.5f) * 2;
    bool edge_mask = max(edge_mask_vec.x, edge_mask_vec.y) >= 0.875f;

    bool grid_mask_small = mod(floor(fragTexCoord.s * 8 + 0.5) + floor(fragTexCoord.t * 8 + 0.5), 2.0f) == 0.0f;

    if (edge_mask && grid_mask_small) {
        int border = calculateBorder();
        if (border > 0) {
            if (border > team_colors.length()) discard;
            fragColor = vec4(team_colors[border - 1], 1.0f);
            return;
        }
    }

    fragColor = texture2D(texture, fragTexCoord);
    if (grid_mask) fragColor *= 0.95f;
}
