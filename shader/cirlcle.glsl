#ifdef GL_ES
precision mediump float;
#endif


uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;


float sstep(float value,float xx){
    return smoothstep(value-0.01*value,value+value*0.1,xx);
}

float circle(vec2 st,float radius){
    vec2 ss = st - vec2(0.5);
    return 1.0-step(radius,dot(ss,ss)*3.0);
}


void main(){
    vec2 st  = gl_FragCoord.xy / u_resolution.xy;
    st.x *= u_resolution.x / u_resolution.y;
    float pct = circle(st,0.4);
    vec4 color = vec4(vec3(pct),1.0);
    gl_FragColor = color;
}