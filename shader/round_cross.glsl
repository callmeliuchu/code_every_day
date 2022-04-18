#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform vec2 u_resolution;

mat2 rotate(float angle){
    return mat2(cos(angle),-sin(angle),
                sin(angle),cos(angle));
}

float box(vec2 st,vec2 size){

    size = vec2(0.5) - 0.5*size;
    vec2 s1 = step(size,st);
    vec2 s2 = step(size,1.0-st);
    return s1.x * s2.x * s2.y * s1.y;
}

float cross(vec2 st,float size){
    return box(st,vec2(size,size/4.0)) + box(st,vec2(size/4.0,size));
}

void main(){
    vec2 st = gl_FragCoord.xy / u_resolution;
    st.x *= u_resolution.x / u_resolution.y;
    st -= 0.5;
    mat2 r = rotate(u_time);
    st = r * st;
    st += 0.3;
    float pct = cross(st,0.25);
    gl_FragColor = vec4(vec3(pct),1.0);
}