#ifdef GL_ES
precision mediump float;
#endif

#define PI 3.1415926
uniform vec2 u_resolution;
uniform float u_time;

float box(vec2 st,vec2 size){
    size = vec2(0.5) - 0.5*size;
    vec2 s1 = step(size,st);
    vec2 s2 = step(size,1.0-st);
    return s1.x * s1.y * s2.x * s2.y;
}

mat2 rotate(float angle){
    // angle = angle / 180.0 * PI;
    return mat2(cos(angle),-sin(angle),
                sin(angle),cos(angle));
}


void main(){
    vec2 st = gl_FragCoord.xy / u_resolution;
    st.x *= u_resolution.x / u_resolution.y;
    st *= 10.0;
    st = fract(st);
    st -= 0.5;
    mat2 r = rotate(u_time);
    st = r * st;
    st += 0.5;
    float pct = box(st,vec2(0.5*sqrt(2.0)));
    vec3 color = vec3(pct);
    gl_FragColor = vec4(color,1.0);
}