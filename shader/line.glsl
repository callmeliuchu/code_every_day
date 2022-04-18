#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;

float plot(vec2 st){
    return smoothstep(0.01,0.0,abs(0.3*sin(st.x*20.0)+0.5-st.y));
}


void main(){
    vec2 st = gl_FragCoord.xy / u_resolution;
    float y = st.x;

    float p = plot(st);
    
    vec3 color = (1.0-p)*vec3(1.0,0.0,0.0) + p*vec3(0.0,1.0,0.0);
    gl_FragColor = vec4(color,1.0);
}