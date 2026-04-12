import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { animate, query, stagger, style, transition, trigger } from '@angular/animations';

import { Itinerary } from './travel.types';

@Component({
  selector: 'app-history-strip',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './history-strip.component.html',
  styleUrl: './history-strip.component.css',
  animations: [
    trigger('historyIn', [
      transition(':enter', [
        query('button', [
          style({ opacity: 0, transform: 'translateX(-16px)' }),
          stagger(55, animate('360ms ease-out', style({ opacity: 1, transform: 'translateX(0)' }))),
        ], { optional: true }),
      ]),
    ]),
  ],
})
export class HistoryStripComponent {
  @Input() plans: Itinerary[] = [];
  @Output() selectPlan = new EventEmitter<Itinerary>();
}
