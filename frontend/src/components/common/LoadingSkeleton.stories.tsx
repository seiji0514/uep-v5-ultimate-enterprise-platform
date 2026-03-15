import type { Meta, StoryObj } from '@storybook/react';
import { LoadingSkeleton } from './LoadingSkeleton';

const meta: Meta<typeof LoadingSkeleton> = {
  component: LoadingSkeleton,
  title: 'Common/LoadingSkeleton',
};
export default meta;

type Story = StoryObj<typeof LoadingSkeleton>;

export const List: Story = {
  args: { variant: 'list', rows: 5 },
};

export const Table: Story = {
  args: { variant: 'table', rows: 6 },
};

export const Card: Story = {
  args: { variant: 'card' },
};

export const Form: Story = {
  args: { variant: 'form' },
};
