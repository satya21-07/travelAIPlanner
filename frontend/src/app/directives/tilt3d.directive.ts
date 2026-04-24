import { Directive, ElementRef, HostListener, Input } from '@angular/core';
import { gsap } from 'gsap';

@Directive({
  selector: '[appTilt3d]',
  standalone: true
})
export class Tilt3dDirective {
  @Input() tiltMax = 15;
  
  constructor(private el: ElementRef) {}

  @HostListener('mousemove', ['$event'])
  onMouseMove(event: MouseEvent) {
    const rect = this.el.nativeElement.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    
    const rotateX = ((y - centerY) / centerY) * -this.tiltMax;
    const rotateY = ((x - centerX) / centerX) * this.tiltMax;

    gsap.to(this.el.nativeElement, {
      duration: 0.5,
      rotateX: rotateX,
      rotateY: rotateY,
      transformPerspective: 1000,
      ease: "power2.out"
    });
    
    // Animate inner content to create a deeper 3D parallax effect
    const img = this.el.nativeElement.querySelector('.img-wrapper');
    const content = this.el.nativeElement.querySelector('.content');
    
    if (img) {
       gsap.to(img, {
         duration: 0.5,
         z: 20,
         ease: "power2.out"
       });
    }
    if (content) {
       gsap.to(content, {
         duration: 0.5,
         z: 40,
         ease: "power2.out"
       });
    }
  }

  @HostListener('mouseleave')
  onMouseLeave() {
    gsap.to(this.el.nativeElement, {
      duration: 1,
      rotateX: 0,
      rotateY: 0,
      ease: "elastic.out(1, 0.3)"
    });
    
    const img = this.el.nativeElement.querySelector('.img-wrapper');
    const content = this.el.nativeElement.querySelector('.content');
    if (img) gsap.to(img, { duration: 1, z: 0, ease: "elastic.out(1, 0.3)" });
    if (content) gsap.to(content, { duration: 1, z: 0, ease: "elastic.out(1, 0.3)" });
  }
}
