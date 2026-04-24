import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Component, OnInit, AfterViewInit, ElementRef, ViewChild, inject } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { gsap } from 'gsap';

import { DestinationGalleryComponent } from './components/destination-gallery/destination-gallery.component';
import { HistoryStripComponent } from './components/history-strip/history-strip.component';
import { ItineraryResultComponent } from './components/itinerary-result/itinerary-result.component';
import { PlannerFormComponent } from './components/planner-form/planner-form.component';
import { TravelStateService } from './services/travel-state.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    HttpClientModule,
    ReactiveFormsModule,
    PlannerFormComponent,
    ItineraryResultComponent,
    DestinationGalleryComponent,
    HistoryStripComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent implements OnInit, AfterViewInit {
  protected readonly state = inject(TravelStateService);

  @ViewChild('shell', { static: false }) shellRef!: ElementRef;
  @ViewChild('ambientOne', { static: false }) ambientOne!: ElementRef;
  @ViewChild('ambientTwo', { static: false }) ambientTwo!: ElementRef;

  ngOnInit(): void {
    this.state.init();
  }

  ngAfterViewInit(): void {
    // Add a 3D ambient parallax effect on mousemove
    document.addEventListener('mousemove', (e) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 2;
      const y = (e.clientY / window.innerHeight - 0.5) * 2;
      
      if (this.ambientOne) {
         gsap.to(this.ambientOne.nativeElement, {
           x: x * 60,
           y: y * 60,
           duration: 2,
           ease: 'power2.out'
         });
      }
      if (this.ambientTwo) {
         gsap.to(this.ambientTwo.nativeElement, {
           x: -x * 45,
           y: -y * 45,
           duration: 2,
           ease: 'power2.out'
         });
      }
    });
  }
}
