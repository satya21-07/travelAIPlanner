import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { animate, query, stagger, style, transition, trigger } from '@angular/animations';

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
        query('button', [
          style({ opacity: 0, transform: 'translateY(24px)' }),
          stagger(60, animate('420ms cubic-bezier(.2,.8,.2,1)', style({ opacity: 1, transform: 'translateY(0)' }))),
        ], { optional: true }),
      ]),
    ]),
  ],
})
export class DestinationGalleryComponent {
  @Input() destinations: Destination[] = [];
  @Output() choose = new EventEmitter<Destination>();
}
