import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
import { animate, style, transition, trigger } from '@angular/animations';

@Component({
  selector: 'app-planner-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './planner-form.component.html',
  styleUrl: './planner-form.component.css',
  animations: [
    trigger('panelIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(22px)' }),
        animate('520ms cubic-bezier(.2,.8,.2,1)', style({ opacity: 1, transform: 'translateY(0)' })),
      ]),
    ]),
  ],
})
export class PlannerFormComponent {
  @Input({ required: true }) form!: FormGroup;
  @Input() loading = false;
  @Input() error = '';
  @Output() submitPlan = new EventEmitter<void>();
}
