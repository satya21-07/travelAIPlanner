import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { animate, query, stagger, style, transition, trigger } from '@angular/animations';

import { DayPlan, Itinerary, PlaceRecommendation } from '../../travel.types';

@Component({
  selector: 'app-itinerary-result',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './itinerary-result.component.html',
  styleUrl: './itinerary-result.component.css',
  animations: [
    trigger('resultIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(24px) scale(.98)' }),
        animate('520ms cubic-bezier(.2,.8,.2,1)', style({ opacity: 1, transform: 'translateY(0) scale(1)' })),
      ]),
    ]),
    trigger('listIn', [
      transition(':enter', [
        query('article, .cost-tile, .tip-line', [
          style({ opacity: 0, transform: 'translateY(18px)' }),
          stagger(70, animate('420ms ease-out', style({ opacity: 1, transform: 'translateY(0)' }))),
        ], { optional: true }),
      ]),
    ]),
  ],
})
export class ItineraryResultComponent {
  private readonly itemSize = 278;
  private readonly visibleCount = 6;
  visibleStart = 0;

  @Input() plan: Itinerary | null = null;

  placeList(plan: Itinerary): PlaceRecommendation[] {
    return plan.places ?? [];
  }

  hasPlaces(plan: Itinerary): boolean {
    return this.placeList(plan).length > 0;
  }

  costItems(plan: Itinerary): [string, number][] {
    return Object.entries(plan.cost_breakdown);
  }

  labelize(value: string): string {
    return value.replace(/_/g, ' ');
  }

  costPercent(plan: Itinerary, value: number): number {
    return Math.max(8, Math.round((value / plan.total_estimated_cost) * 100));
  }

  onTimelineScroll(event: Event): void {
    const scrollTop = (event.target as HTMLElement).scrollTop;
    const nextStart = Math.floor(scrollTop / this.itemSize);
    if (nextStart !== this.visibleStart) {
      this.visibleStart = nextStart;
    }
  }

  renderedDays(plan: Itinerary): DayPlan[] {
    return plan.daily_plan.slice(this.visibleStart, this.visibleStart + this.visibleCount);
  }

  topSpacerHeight(): number {
    return this.visibleStart * this.itemSize;
  }

  bottomSpacerHeight(plan: Itinerary): number {
    const rendered = this.renderedDays(plan).length;
    return Math.max(0, (plan.daily_plan.length - this.visibleStart - rendered) * this.itemSize);
  }
}
