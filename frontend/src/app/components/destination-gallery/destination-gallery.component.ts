import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output, ElementRef, ViewChild, AfterViewInit, OnChanges, SimpleChanges } from '@angular/core';
import { animate, query, stagger, style, transition, trigger } from '@angular/animations';
import { gsap } from 'gsap';

import { Destination } from '../../travel.types';

@Component({
  selector: 'app-destination-gallery',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './destination-gallery.component.html',
  styleUrl: './destination-gallery.component.css',
  animations: [
    trigger('galleryIn', [
      transition(':enter', [
        query('.carousel-wrapper', [
          style({ opacity: 0, transform: 'translateY(24px)' }),
          animate('420ms cubic-bezier(.2,.8,.2,1)', style({ opacity: 1, transform: 'translateY(0)' }))
        ], { optional: true }),
      ]),
    ]),
  ],
})
export class DestinationGalleryComponent implements AfterViewInit, OnChanges {
  readonly fallbackImage = 'assets/destination-fallback.svg';

  @Input() destinations: Destination[] = [];
  @Output() choose = new EventEmitter<Destination>();

  @ViewChild('carousel3d', { static: false }) carousel3d!: ElementRef;
  
  rotation = 0;
  theta = 0;
  radius = 0;

  isDragging = false;
  dragged = false;
  startX = 0;
  startRotation = 0;

  ngAfterViewInit() {
    this.setupCarousel();
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['destinations'] && !changes['destinations'].isFirstChange()) {
      setTimeout(() => this.setupCarousel(), 0);
    }
  }

  setupCarousel() {
    if (!this.carousel3d || this.destinations.length === 0) return;
    
    const items = this.carousel3d.nativeElement.querySelectorAll('.carousel-item');
    const numItems = items.length;
    this.theta = 360 / numItems;
    
    // approximate item width 300px
    const itemWidth = 300;
    this.radius = Math.round((itemWidth / 2) / Math.tan(Math.PI / numItems)) + 60; // extra padding

    gsap.set(this.carousel3d.nativeElement, { z: -this.radius });

    items.forEach((item: HTMLElement, i: number) => {
      // We must use raw CSS transform to ensure rotateY happens before translateZ
      // GSAP's translate -> rotate order will not form a proper circular carousel.
      item.style.transform = `rotateY(${i * this.theta}deg) translateZ(${this.radius}px)`;
    });
  }

  onDragStart(event: MouseEvent | TouchEvent) {
    this.isDragging = true;
    this.dragged = false;
    this.startX = this.getClientX(event);
    this.startRotation = this.rotation;

    // Stop current animation immediately
    gsap.killTweensOf(this.carousel3d.nativeElement);
  }

  onDragMove(event: MouseEvent | TouchEvent) {
    if (!this.isDragging) return;
    
    const currentX = this.getClientX(event);
    const diff = currentX - this.startX;
    
    if (Math.abs(diff) > 5) {
      this.dragged = true;
    }

    // Multiply by a factor for comfortable rotation speed
    this.rotation = this.startRotation + (diff * 0.4);
    
    gsap.set(this.carousel3d.nativeElement, {
      rotationY: this.rotation,
      z: -this.radius,
    });
  }

  onDragEnd() {
    if (!this.isDragging) return;
    this.isDragging = false;
    
    // Snap to the nearest carousel item
    if (this.theta > 0) {
      this.rotation = Math.round(this.rotation / this.theta) * this.theta;
      gsap.to(this.carousel3d.nativeElement, { 
        rotationY: this.rotation, 
        z: -this.radius,
        duration: 0.8, 
        ease: 'power3.out' 
      });
    }
  }

  getClientX(event: MouseEvent | TouchEvent): number {
    return 'touches' in event ? event.touches[0].clientX : (event as MouseEvent).clientX;
  }

  onItemClick(event: Event, destination: Destination) {
    if (this.dragged) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }
    this.choose.emit(destination);
  }

  useFallbackImage(event: Event): void {
    const image = event.target as HTMLImageElement | null;
    if (!image || image.src.endsWith(this.fallbackImage)) {
      return;
    }
    image.src = this.fallbackImage;
  }
}
